from streamlit.web import bootstrap


def main():
    real_script = './pages/4_db_analyze.py'
    #real_script = 'main.py'
    #real_script = 'main.py'

    bootstrap.run(real_script, f'run.py {real_script}', [], {})


if __name__ == "__main__":
    main()