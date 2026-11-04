#!/usr/bin/env bash
# Veb + Telegram-botni fonda ishga tushiradi / to'xtatadi.
#   ./run.sh start | stop | restart | status | log
cd "$(dirname "$0")"
PID=data/agent.pid
LOG=data/agent.log

start() {
  if [ -f "$PID" ] && kill -0 "$(cat "$PID")" 2>/dev/null; then echo "Ishlayapti (pid $(cat $PID))"; return; fi
  [ -f data/uzex.duckdb ] || .venv/bin/python prepare.py
  nohup .venv/bin/python main.py >>"$LOG" 2>&1 &
  echo $! >"$PID"
  echo "Ishga tushdi (pid $!), log: $LOG, veb: http://localhost:${WEB_PORT:-8000}"
}
stop() {
  [ -f "$PID" ] && kill "$(cat "$PID")" 2>/dev/null && echo "To'xtatildi"
  rm -f "$PID"
}
case "$1" in
  start) start ;;
  stop) stop ;;
  restart) stop; sleep 1; start ;;
  status) [ -f "$PID" ] && kill -0 "$(cat "$PID")" 2>/dev/null && echo "Ishlayapti (pid $(cat $PID))" || echo "To'xtagan" ;;
  log) tail -f "$LOG" ;;
  *) echo "Foydalanish: $0 start|stop|restart|status|log" ;;
esac
