# Nova Study Coach v0.2

Nova is a small local study and project coach. It accepts typed messages, suggests one main task for today, offers one optional task, gives one practical tip, and stores lightweight progress in a local JSON file.

## What v0.2 includes
- Local command-line interface
- Local browser web UI
- Python coach backend
- Local JSON memory in `data/nova_memory.json`
- Study and side-project planning support
- Beginner-friendly deterministic behavior

## What v0.2 does not include
- AI model integration
- Database
- Cloud deployment
- User accounts
- Voice input
- Required voice output

## Run the CLI
```bash
python -m nova.cli
```

You can type messages such as:
```text
I want to learn AI agents this week.
I only have 30 minutes today.
What should I do next?
I feel lazy today.
Plan my project process.
```

Exit with:
```text
exit
```

## Run the local web UI
```bash
python -m nova.web
```

Then open:
```text
http://127.0.0.1:8765
```

## Run tests
```bash
python -m pytest
```

## Memory
Nova stores local memory in:
```text
data/nova_memory.json
```

The file is created automatically if it does not exist.
