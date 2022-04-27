# WAF-AI

WAF-AI is a easy to use containerised WAF powered by an XGBoost machine learning model.

To download and run the container:

1. Clone the repo (Notebooks folder not required - available just to show how the ML model is built.
2. Run the command `docker-compose up -d` to build and run the container (-d option to enable detach mode).
3. A flask application served by gunicron and nginx will start on the localhost (perfect for cloud hosting).
4. Send any HTTP request to http://localhost/predict endpoint (http://{public-ip}/predict if hosted on a cloud environment)
5. WAF-AI will analyse the request and return either 'good' or 'bad'. If bad the user should not allow that request to proceed to their web app.
