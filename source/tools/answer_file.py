#!/bin/python3
import yaml

newline = '\r'
answer_file = 'answer_file.yaml'
auto_setup = 'auto_setup.sh'
pass_along = 'pass_along'
file = []

with open(answer_file) as stream:
    answers = yaml.safe_load(stream)

file.append('cd ../')
file.append(pass_along + '=True')
file.append('export ' + pass_along)
for answer in answers:
    file.append(str(answer) + '=' + answers[answer])
    file.append('export ' + answer)
file.append('./setup.sh')

for line in file:
    print(line)

with open(auto_setup, 'w+') as data:
    data.write(newline.join(file))
