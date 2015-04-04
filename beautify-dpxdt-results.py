import glob
import os.path
import argparse
import json
import re
import pprint
from quik import FileLoader


def readTestResult(log_file):
  pattern = re.compile("all:\s([-+]?[0-9]*\.?[0-9]+)\s\(([-+]?[0-9]*\.?[0-9]+)\)")
  difference_abs = 0
  difference_rel = 0
  for i, line in enumerate(open(log_file)):
    for match in re.finditer(pattern, line):
      difference_abs = float(match.group(1))
      difference_rel = float(match.group(2))
  class_name = 'succeeded' if (difference_abs == 0) else 'failed'
  return {'succeeded': (difference_abs == 0), 'difference' : difference_rel, 'className': class_name}


def readTest(config_file):
  base_path = os.path.dirname(config_file)
  folder_name = os.path.basename(base_path)
  raw_json_data=open(config_file).read()
  data = json.loads(raw_json_data)

  test = {
    'config': data,
    'config_formatted' : pprint.pformat(data, indent=2, width=1),
    'result': readTestResult(base_path + '/log.txt'),
    'base_image' : base_path + '/ref_resized',
    'current_image' : base_path + '/screenshot.png',
    'diff_image': base_path + '/diff.png',
    'filename': folder_name + "-" + data['targetUrl'].replace('http://','').replace('/', '-') + '.html'
  }

  return test;


def scanTests(directory):
  tests = []

  config_files = glob.glob(directory + '/*/*/config.json')

  for config_file in config_files:
    tests.append(readTest(config_file))

  return tests


def main():

  parser = argparse.ArgumentParser(description='Beautify dpxdt-results.')
  parser.add_argument('directory',help='directory with dpxdt-results',action='store')

  args = parser.parse_args()

  tests = scanTests(args.directory)

  loader = FileLoader(os.path.dirname(__file__) + '/templates')
  template = loader.load_template('result.html')
  for test in tests:
    content = template.render(test, loader=loader).encode('utf-8')
    result_file = open(test['filename'], "w")

    result_file.write(content)
    result_file.close()

    print "Created " + test['filename'] + "..."

  template = loader.load_template('index.html')
  content = template.render({ 'tests': tests }, loader=loader).encode('utf-8')

  result_file = open('index.html', "w")
  result_file.write(content)
  result_file.close()

  print "Created inde.html ..."


if __name__ == "__main__":
    main()
