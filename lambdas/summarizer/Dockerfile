FROM public.ecr.aws/lambda/python:3.12

# Copy shared package
COPY ../shared ${LAMBDA_TASK_ROOT}/lambdas/shared

# Copy slides package (needed for generate_outline)
COPY ../slides ${LAMBDA_TASK_ROOT}/lambdas/slides

# Copy summarizer package
COPY . ${LAMBDA_TASK_ROOT}/lambdas/summarizer

# Install dependencies
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/lambdas/summarizer/requirements.txt

CMD ["lambdas.summarizer.handler.handler"]
