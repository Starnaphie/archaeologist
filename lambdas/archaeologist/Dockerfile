FROM public.ecr.aws/lambda/python:3.12

# Install git for repo cloning
RUN dnf install -y git && dnf clean all

# Copy shared package first so it is available as lambdas.shared
COPY ../shared ${LAMBDA_TASK_ROOT}/lambdas/shared

# Copy archaeologist package
COPY . ${LAMBDA_TASK_ROOT}/lambdas/archaeologist

# Install dependencies
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/lambdas/archaeologist/requirements.txt

# Set handler
CMD ["lambdas.archaeologist.handler.handler"]
