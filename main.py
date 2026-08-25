"""Convert EchoTrace chat-export JSON files to readable TXT files."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Iterable


def get_app_dir() -> Path:
	"""Return the directory used for input and output files."""
	file_dir = os.path.dirname(os.path.abspath(__file__))
	if getattr(sys, "frozen", False):
		return Path(sys.executable).resolve().parent
	return Path(file_dir)


def load_messages(json_path: Path) -> list[dict[str, Any]]:
	"""Load and validate the messages array from an EchoTrace export."""
	try:
		with json_path.open("r", encoding="utf-8-sig") as file:
			data = json.load(file)
	except json.JSONDecodeError as error:
		raise ValueError(f"JSON 格式无效：{error}") from error

	if not isinstance(data, dict) or not isinstance(data.get("messages"), list):
		raise ValueError("JSON 中未找到有效的 messages 消息数组")

	return [message for message in data["messages"] if isinstance(message, dict)]


def format_message(message: dict[str, Any]) -> str:
	"""Format one message while keeping its time, sender, and content."""
	message_time = str(message.get("formattedTime") or message.get("createTime", "未知时间"))
	sender = str(message.get("senderDisplayName") or message.get("senderUsername", "未知发送人"))
	content = str(message.get("content", ""))
	return f"[{message_time}] {sender}: {content}"


def convert_messages(messages: Iterable[dict[str, Any]]) -> str:
	"""Convert messages to UTF-8 text with one message per line."""
	return "\n".join(format_message(message) for message in messages) + "\n"


def convert_file(json_path: Path, output_path: Path | None = None) -> Path:
	"""Convert one JSON file and return the generated TXT path."""
	output_path = output_path or json_path.with_suffix(".txt")
	output_path.write_text(convert_messages(load_messages(json_path)), encoding="utf-8")
	return output_path


def find_json_files(input_path: Path) -> list[Path]:
	"""Find JSON files from a file path or a directory."""
	if input_path.is_file():
		if input_path.suffix.lower() != ".json":
			raise ValueError("输入文件必须是 .json 文件")
		return [input_path]
	if input_path.is_dir():
		return sorted(path for path in input_path.glob("*.json") if path.is_file())
	raise FileNotFoundError(f"找不到输入路径：{input_path}")


def wait_for_exit() -> None:
	"""Keep a double-clicked console window open until the user presses a key."""
	try:
		input("\n按任意键退出...")
	except EOFError:
		pass


def main() -> int:
	app_dir = get_app_dir()
	parser = argparse.ArgumentParser(description="将 EchoTrace 聊天记录 JSON 转换为 TXT")
	parser.add_argument(
		"input",
		nargs="?",
		type=Path,
		default=None,
		help="JSON 文件或目录，默认是 EXE 所在目录",
	)
	args = parser.parse_args()
	input_path = app_dir if args.input is None else args.input
	if not input_path.is_absolute():
		input_path = app_dir / input_path

	result = 0
	try:
		json_files = find_json_files(input_path)
		if not json_files:
			print(f"目录中没有找到 JSON 文件：{input_path}")
			result = 1
		else:
			converted_count = 0
			failed_count = 0
			for json_file in json_files:
				try:
					output_file = convert_file(json_file)
					print(f"已生成：{output_file.name}")
					converted_count += 1
				except (OSError, ValueError) as error:
					print(f"转换失败：{json_file.name}：{error}", file=sys.stderr)
					failed_count += 1
			print(f"\n处理完成：成功 {converted_count} 个，失败 {failed_count} 个")
			result = 1 if failed_count else 0
	except (OSError, ValueError) as error:
		print(f"转换失败：{error}", file=sys.stderr)
		result = 1
	return result


if __name__ == "__main__":
	try:
		exit_code = main()
	finally:
		wait_for_exit()
	raise SystemExit(exit_code)
