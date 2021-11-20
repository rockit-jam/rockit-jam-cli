# rockit-jam
Rockit start JAMstack application!


```
rockit init

rockit analyze

rockit build
 => including analyze command.

rockit deploy
 => must be rockit build first.

rockit local
 => alias to  rockit build --vendor dev & rockit deploy --vendor dev


rockit init


rockit scaffold --template=sam-http --name=api

rockit scaffold --template=vuetify-gui --name=gui

rockit scaffold --template=dynamodb --name=kvdb

rockit join --name=api

rockit join --name=gui

rockit join --name=kvdb

rockit local

rockit local --name=api

rockit synth

rockit deploy
```

```
mkdir <appdir>
cd <appdir>

npm i aws-cdk@next

mkdir cdk
cd cdk
npx cdk init app --language=python

sam-beta-cdk init --name api --runtime python3.8


```

```
cd <appdir>
cd api
sam-beta-cdk local start-api
```

```
cd <appdir>
rockit build --name=api
```

```
mkdir <appdir>
cd <appdir>
python3.8 -m venv --without-pip .venv
source .venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
cd cdk
pip install -r requirements.txt

cd ..
pip install pyyaml
```

```

npx cdk synth -a "python gen-template.py" > api/template.yaml

cd api
sam-beta-cdk local start-api
```

```
cd api
sam-beta-cdk build
# .aws-sam/build にビルド結果が出力される

