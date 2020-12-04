### dashboard.github.io

http://dashboard-env-1.eba-szsfmavw.us-east-2.elasticbeanstalk.com/

1. Tech stacks:
    - Dash (Plotly)
    - AWS CodePipeline
    - AWS Elastic Beanstalk
    - AWS RDS (MySQL)
2. User guide:
    - operations:
        1. Create:
            - download template dashcode
            - A signal_id will be given
            - upload and display the template dashcode
        2. Read:
            - display dashcode
        3. Modify:
            - upload and display dashcode
            - update signal info in db
        4. Delete:
            - delete dashcode and signal in db

---
Notes:
1. Issues when deploying the dashboard on Elastic Beanstalk:
    - Port number must align with the one Elastic Beanstalk is using.
      you can check EB log for the information.
    - File name must be ***application.py***
    - Must use ***application=app.server*** and ***application.run***
    - Keep the requirements.txt is concise as possible
2. Development steps:
    - Write some dashcode for figures
    - Gen html for embed
    - Host the html files on GitHub Page and get the URLs.
    - Embed the URLs in application.py 
    - upload application.zip to Elastic Beanstalk
        - any changes on GitHub will trigger the upload process (AWS CodePipeline)