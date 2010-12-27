#include "Python.h"

static PyObject *
hello_tool(PyObject *self, PyObject *args)
{
    return Py_BuildValue("s", "Hello cli!");
}

static PyMethodDef
module_functions[] = {
    { "hello_tool", hello_tool, METH_VARARGS, "Say hello." },
    { NULL }
};

void
init_tools(void)
{
    Py_InitModule3("_tools", module_functions, "A minimal module.");
}
