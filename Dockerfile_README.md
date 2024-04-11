# SQLProbe

## Source

https://github.com/KhulnaSoft-Lab/sqlprobe
 
## Usage:

```bash
cd sqlprobe/
docker build -t sqlprobe .
docker run -it sqlprobe:latest
```

## Help
```bash
docker run -it sqlprobe -d <SQLI DORK> -e <SEARCH ENGINE>
docker run -it sqlprobe -t <URL>    
```
