# Unix

> **Purpose:** Unix/Linux commands, shell basics, file management, permissions, text processing, networking, and process management.
> **Use this file for:** backend, DevOps, data engineering, and production support interviews

---

## Recommended Study Flow

1. Read the **Quick Summary** first.
2. Review the **Key Concepts** and tables.
3. Practice the **Interview Questions & Answers** out loud.
4. Use the code snippets and examples to explain trade-offs clearly.
5. Finish with the **Common Mistakes** and **Revision Checklist** sections.

---

## Quick Summary

Unix commands are used to manage files, inspect logs, debug services, automate tasks, and operate production systems. For interviews, focus on file commands, permissions, process inspection, text processing, pipes, and networking.

---

## Command Categories

| Category          | Commands                                              |
| ----------------- | ----------------------------------------------------- |
| Files/directories | `ls`, `cd`, `pwd`, `mkdir`, `cp`, `mv`, `rm`, `touch` |
| File content      | `cat`, `less`, `head`, `tail`, `grep`, `sed`, `awk`   |
| System info       | `uname`, `top`, `ps`, `df`, `du`, `free`              |
| Networking        | `ping`, `ip`, `netstat`/`ss`, `curl`, `wget`          |
| Permissions       | `chmod`, `chown`, `chgrp`                             |
| Compression       | `tar`, `gzip`, `gunzip`, `zip`, `unzip`               |
| Processes         | `kill`, `jobs`, `fg`, `bg`, `ps`, `top`               |
| Text processing   | `sort`, `uniq`, `wc`, `cut`, `tr`                     |

---

## Interview Questions & Answers
### Q1. How do you find errors in a log file?

```bash
grep -i "error" app.log
```

For live logs:

```bash
tail -f app.log | grep -i "error"
```

### Q2. How do you check disk usage?

```bash
df -h      # file system usage
du -sh *   # directory/file sizes
```

### Q3. How do you check running processes?

```bash
ps aux | grep python
top
```

### Q4. How do you change file permissions?

```bash
chmod 755 script.sh
chmod 644 config.txt
```

### Q5. What is a pipe?

A pipe sends the output of one command as input to another command.

```bash
cat app.log | grep ERROR | wc -l
```

### Q6. What is the difference between `>` and `>>`?

- `>` overwrites a file.
- `>>` appends to a file.

```bash
echo "hello" > file.txt
echo "again" >> file.txt
```

---

## Common Production Debugging Commands

```bash
curl -I https://example.com
curl -X POST https://api.example.com/health
ps aux | grep uvicorn
netstat -tulpn
ss -tulpn
tail -n 100 app.log
grep -R "DATABASE_URL" .
```

---

## Revision Checklist

- [ ] File and directory commands
- [ ] Permissions and ownership
- [ ] grep, sed, awk
- [ ] Pipes and redirection
- [ ] Process inspection
- [ ] Disk and memory checks
- [ ] curl and networking basics
