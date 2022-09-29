from streamlit.web import bootstrap


def main():
    real_script = './pages/2_ma_detail.py'

    bootstrap.run(real_script, f'run.py {real_script}', [], {})


if __name__ == "__main__":
    main()