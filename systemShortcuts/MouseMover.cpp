#include <stdlib.h>
#include <unistd.h>

#ifdef _WIN32
#include <windows.h>
int main() {
  chdir("./MouseMoverData");
  WinExec("./MouseMover.exe", SW_HIDE);
  return 0;
}

#endif

#ifdef linux

int main() {
  chdir("./MouseMoverData/");
  system("./MouseMover");
  return 0;
}
#endif
