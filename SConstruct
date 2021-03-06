
import os
from build.scons.util import *

# read variables from the cache, a user's custom.py file or command line arguments
vars = Variables(['variables.cache', 'custom.py'], ARGUMENTS)
vars.Add(BoolVariable('debug', 'Debug build', 'no'))
vars.Add(BoolVariable('edebug', 'Extreme Debug build', 'no'))

vars.Add(EnumVariable('default_compiler', 'Preferred compiler', 'g++', allowed_values=('g++', 'clang++')))
vars.Add(PathVariable('lwpr', 'Path to lwpr sources', os.getcwd(), PathVariable.PathIsDir))
vars.Add(PathVariable('prefix', 'Path where the FS library is to be installed', '.', PathVariable.PathIsDir))

env = Environment(variables=vars, ENV=os.environ)
env['CXX'] = os.environ.get('CXX', env['default_compiler'])


# Set up some directories
env['src'] = os.path.join(env['lwpr'], 'src')
env['vendor'] = os.path.join(env['lwpr'], 'vendor')
env['build_basename'] = '.build'


if env['edebug']:
    build_suffix = 'edebug'
elif env['debug']:
    build_suffix = 'debug'
else:
    build_suffix = 'prod'
build_dirname = os.path.join(env['build_basename'], build_suffix)
env.VariantDir(build_dirname, '.')

Help(vars.GenerateHelpText(env))
vars.Save('variables.cache', env)

# Base include directories
include_paths = ['include']
isystem_paths = []

# Possible modules
# Compilation flag, module name, use-by-default?
modules = [
    ("core",           "core")
]

# include local by default # MRJ: This probably should be acquired from an environment variable
isystem_paths += ['/usr/local/include', os.path.expanduser('~/local/include')]


# Process modules and external dependencies
sources = []
module_headers = []
for flag, modname in modules:
    if flag not in env or env[flag]:  # Import module if not explicitly disallowed
        print("Importing module: \"{}\"".format(modname))
        headers = []
        SConscript('build/scons/{}.sconscript'.format(modname), exports="env sources headers")
        module_headers += [(os.path.join('lwpr', modname), headers)]
        print(module_headers)
    else:
        print("Skipping module \"{}\"".format(modname))


env.Append( CPPPATH = [ os.path.abspath(p) for p in include_paths ] )
env.Append( CCFLAGS = [ '-isystem' + os.path.abspath(p) for p in isystem_paths ] )


# Determine all the build files
static_libname = env['libname'] + "-static"
build_files = [os.path.join(build_dirname, src) for src in sources]
shared_lib = env.SharedLibrary(os.path.join(env['build_basename'], env['libname']), build_files)
static_lib = env.StaticLibrary(os.path.join(env['build_basename'], static_libname), build_files)
deployed_lib = env.Install(os.path.join(env['prefix'], 'lib'), shared_lib)
deployed_headers = [env.Install(os.path.join(env['prefix'], 'include', mod_prefix), headers) for mod_prefix, headers in module_headers]
env.Alias('install', [deployed_lib] + deployed_headers)
# Save a description of the compilation and linking options to be used when linking the final solver
save_pkg_config_descriptor(env, env['libname'], '{}.pc'.format(env['libname']))

Default([shared_lib])
#Default([static_lib, shared_lib])
