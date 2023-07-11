find_package(PythonInterp)
if(PYTHONINTERP_FOUND)
  get_filename_component(_python_path ${PYTHON_EXECUTABLE} PATH)
  find_program(CYTHON_EXECUTABLE
               NAMES cython cython.bat cython3
               HINTS ${_python_path}
               DOC "path to the cython executable")
else()
  find_program(CYTHON_EXECUTABLE
               NAMES cython cython.bat cython3
               DOC "path to the cython executable")
endif()

if(CYTHON_EXECUTABLE)
  set(CYTHON_version_command ${CYTHON_EXECUTABLE} --version)

  execute_process(COMMAND ${CYTHON_version_command}
                  OUTPUT_VARIABLE CYTHON_version_output
                  ERROR_VARIABLE CYTHON_version_error
                  RESULT_VARIABLE CYTHON_version_result
                  OUTPUT_STRIP_TRAILING_WHITESPACE)

  if(NOT ${CYTHON_version_result} EQUAL 0)
    set(_error_msg "Command \"${CYTHON_version_command}\" failed with")
    set(_error_msg "${_error_msg} output:\n${CYTHON_version_error}")
    message(SEND_ERROR "${_error_msg}")
  else()
    if("${CYTHON_version_output}" MATCHES "^[Cc]ython version ([^,]+)")
      set(CYTHON_VERSION "${CMAKE_MATCH_1}")
    endif()
  endif()
endif()

include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(Cython REQUIRED_VARS CYTHON_EXECUTABLE)

mark_as_advanced(CYTHON_EXECUTABLE)

include(UseCython)
