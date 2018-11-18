from string import Template
import os

pc_template = """
prefix=${lwpr}
exec_prefix=${prefix}
includedir=${prefix}/include
libdir=${exec_prefix}/lib

Name: ${libname}
Description: The Dilithium Dynamic Programming library
Version: 0.0.1
Cflags: ${compile_flags} ${include_paths} -I${includedir}
Libs: ${link_flags} ${lib_paths} -L${libdir} ${libs}
"""


def save_pkg_config_descriptor( env, libname, filename ) :

    with open( filename, 'w' ) as outstream :
        mapping = {}
        # MRJ: @TODO figure out if there's a way to retrieve the "translated" Flags out of the Scons environment
        mapping['prefix'] = env['prefix']
        mapping['exec_prefix'] = '${exec_prefix}'
        mapping['includedir'] = '${includedir}'
        mapping['libdir'] = '${libdir}'
        mapping['lwpr'] = env['lwpr']
        mapping['libname'] = libname

        mapping['compile_flags'] = env['CCFLAGS']
        mapping['include_paths'] = ' '.join([ '-I{}'.format(path) for path in env['CPPPATH'] ])
        mapping['link_flags'] = env['LINKFLAGS']
        mapping['libs'] = ' '.join([ '-l{}'.format(name) for name in env['LIBS'] ] + [ '-l{}'.format(libname) ])
        mapping['lib_paths'] = ' '.join([ '-L{}'.format(path) for path in env['LIBPATH'] ])
        pc = Template(pc_template)
        outstream.write(pc.substitute(mapping))
