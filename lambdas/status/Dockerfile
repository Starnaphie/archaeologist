FROM public.ecr.aws/lambda/python:3.12
COPY . ${LAMBDA_TASK_ROOT}/lambdas/status
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/lambdas/status/requirements.txt
CMD ["lambdas.status.handler.handler"]
