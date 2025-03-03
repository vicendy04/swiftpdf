# swiftpdf

## Design api

Task Creation

```js
    POST /api/tasks
    
    Status: 202 Accepted
    Content-Type: application/json

	{
	    "tool": "merge",
	    "input_files": [
	        "cErdvQ7PT3.pdf",
	        "3oK3kHA8cR.pdf"
	    ]
	}

	{
	    "task_id": "123",
	    "status": "pending",
	    "tool": "merge",
	    "created_at": "2025-01-01T12:12:12.910933Z",
	    "completed_at": null,
	    "input_files": [
	        "cErdvQ7PT3.pdf",
	        "3oK3kHA8cR.pdf"
	    ],
	    "output_files": [],
	    "error": null,
	    "ranges": []
	}

```

Task Status

```js
    GET /api/tasks/123
    
    Status: 200 OK
    Content-Type: application/json
    
	{
	    "task_id": "123",
	    "status": "completed",
	    "tool": "merge",
	    "created_at": "2025-01-01T12:12:12.910933Z",
	    "completed_at": "2025-01-01T12:12:13Z",
	    "input_files": [
	        "cErdvQ7PT3.pdf",
	        "3oK3kHA8cR.pdf"
	    ],
	    "output_files": "uDh9A6WWth_merged.pdf",
	    "error": null,
	    "ranges": []
	}

```

## Steps

1. **Initialize File Upload**
    
    - Client calls `GET /files` to prepare for file upload.
    - `uuid` is generated to encrypt the real filename.
    - Response contains `public_filename` and `url` for uploading.

2. **Upload File**
    
    - Client uploads the file to the provided `url`.
    - Upon success, display a mode window.

3. **Create Task**
    
    - Client submits a request to create a task.
    - Response: `taskId` (e.g., `123`).

4. **Check Task Status**

    - Client retrieves task status using

    ```
        GET /tasks/{task_id}
    ```

5. **Download Merged File**

    - Once the task is complete, client fetches the result

    ```
        GET /files/{output_id}
    ```

    - The file is downloaded in a ZIP format.

