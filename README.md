### dashboard.github.io
1. Tech stacks:
    - Dash (Plotly)
    - AWS Elastic Beanstalk (EB)
    - AWS CodePipeline
2. User guide:
    - operations: [input(s)]
        1. Create: [user_id]
            - A dashcode template will be downloaded
            - A signal_id will be given
            - The template dashboard will be uploaded and displayed
        2. Read: [user_id; signal_id]
            - A dashcode will be read
            - The dashcode will be displayed
        3. Modify: [user_id; signal_id; dashcode]
            - The dashcode will be uploaded and displayed
        4. Delete: [user_id; signal_id]
            - The corresponding dashcode will be deleted

---
Notes:
1. Issues when deploying the dashboard on EB:
    - Port number must align with the one EB is using.
      you can check EB log for the information.
    - File name must be ***application.py***
    - Must use ***application=app.server*** and ***application.run***
    - Keep the requirements.txt is concise as possible
2. Development steps:
    - Write some dashcode for figures
    - Gen html for embed
    - Host the html files on github.io. get URLs.
    - Embed the URLs in application.py
    - Upload application.zip to EB
 3. Other info:
    - TBD