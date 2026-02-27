from train import run_training_pipeline


if __name__ == "__main__":
    print("Starting ML Training Pipeline inside Docker")

    run_training_pipeline()

    print("Pipeline completed successfully")