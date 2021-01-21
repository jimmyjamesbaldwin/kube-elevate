FROM python:3.7
RUN pip install kopf kubernetes
RUN mkdir /templates
COPY handlers.py /handlers.py
COPY templates/role.yaml /templates/role.yaml
COPY templates/rolebinding.yaml /templatesrolebinding.yaml
CMD kopf run --standalone /handlers.py