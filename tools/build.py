# Build ACSUtils and compile it with all supported compilers
# Example .bat file to call this from:

# set ACC_DIR=C:\path\to\acc\
# set BCC_DIR=C:\path\to\bcc\
# set GDCC_DIR=C:\path\to\gdcc\
# python3 build.py

import os, shutil, sys, subprocess
import changeflaggen, preprocess

def run_compiler(name, executable, cmpExtension, exArgs = ''):
	envVarName = name + "_DIR"
	path = ''
	try:
		path = os.environ[envVarName]
	except Exception:
		print(name + ' not specified')
		return

	if sys.platform == 'win32':
		executable += '.exe'

	try:
		subprocess.check_call([os.path.join(path, executable), '-i', 'dist/', 'misc/empty_project.' + cmpExtension, f'acs/{name}.o', exArgs]);
	except Exception:
		print(name + ' failed')
		return

	print(name + ' succeeded')

def main():
	if os.path.isdir('acs'):
		shutil.rmtree('acs')

	os.mkdir('acs')

	if os.path.isdir('dist'):
		shutil.rmtree('dist')

	os.mkdir('dist')

	shutil.copy('misc/cvarinfo.acsutils', 'dist/')
	shutil.copy('misc/decorate.acsutils', 'dist/')

	try:
		preprocess.main();
	except Exception as e:
		print(f'preprocess.py failed, exception thrown: {e}')

	try:
		changeflaggen.main();
	except Exception as e:
		print(f'changeflaggen.py failed, exception thrown: {e}')


	print('Test compiling ACSUtils...')
	run_compiler('ACC', 'acc', 'acs')
	run_compiler('BCC', 'zt-bcc', 'acs')
	run_compiler('GDCC', 'gdcc-acc', 'acs', '--no-warn-forward-reference')

	print('Test compiling BCSUtils...')
	run_compiler('BCC', 'zt-bcc', 'bcs')

if __name__ == '__main__':
	main()
