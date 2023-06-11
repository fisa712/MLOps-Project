from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('example_CRAFT_dag', default_args=default_args, schedule_interval='@daily')

t1 = BashOperator(
    task_id='clone_repo',
    bash_command='git clone https://github.com/clovaai/CRAFT-pytorch.git ~/CRAFT-pytorch',
    dag=dag
)

t2 = BashOperator(
    task_id='install_dependencies',
    bash_command='pip install torch torchvision opencv-python',
    dag=dag
)

t3 = BashOperator(
    task_id='run_craft',
    bash_command='python ~/CRAFT-pytorch/test.py --trained_model=craft_mlt_25k.pth --test_folder=/home/abdullah/Desktop/datasetcraft --output_folder=/home/abdullah/Desktop/datasetcraftouput',
    dag=dag
)

t3.set_upstream(t1)
t3.set_upstream(t2)