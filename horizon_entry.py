from prefect import flow

@flow
def code_review_flow():
    print("Flow registered successfully")