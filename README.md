# omamori-finder-v2

## 1. Run the server

### 1.a Development

1. Open Docker Desktop.

2. To run the server in development, we use a Docker container. Before running the container, set your AWS credentials as environment variables.

   In a `bash` terminal, run the following `export` commands (found under _Option 1: Set AWS environment variables_) after logging in through the access portal:

   ```bash
   export AWS_ACCESS_KEY_ID="aws-access-key-id"
   export AWS_SECRET_ACCESS_KEY="aws-secret-access-key"
   export AWS_SESSION_TOKEN="aws-session-token"
   ```

 3. Once your environment variables are set, start the container by running:
```bash
docker compose up
```
To run without logs:
```bash
docker compose up -d
```