FROM public.ecr.aws/lambda/python:3.12
COPY ../shared ${LAMBDA_TASK_ROOT}/lambdas/shared
COPY . ${LAMBDA_TASK_ROOT}/lambdas/url_generator
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/lambdas/url_generator/requirements.txt
CMD ["lambdas.url_generator.handler.handler"]
