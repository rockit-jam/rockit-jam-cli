def _exec_deploy(args: argparse.Namespace) -> int:
    print("deploy")

    env = {"CDK_MODE": "local"}
    env.update(os.environ)
    with open(Path("api") / "template.yaml", "w") as f:
        subprocess.run(["npx", "cdk", "synth"], env=env, stdout=f, cwd=Path("cdk"))

    subprocess.run(["sam", "build"], cwd=Path("api"))

    subprocess.run(["npx", "cdk", "deploy"], cwd=Path("cdk"))
