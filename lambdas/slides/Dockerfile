FROM public.ecr.aws/lambda/python:3.12

# Copy shared package
COPY ../shared ${LAMBDA_TASK_ROOT}/lambdas/shared

# Copy slides package
COPY . ${LAMBDA_TASK_ROOT}/lambdas/slides

# Install dependencies
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/lambdas/slides/requirements.txt

CMD ["lambdas.slides.handler.handler"]
