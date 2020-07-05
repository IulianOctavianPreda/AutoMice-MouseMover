from build import Build

import shutil

if __name__ == "__main__":
    appBuilder = Build()
    appBuilder.build()
    shutil.make_archive(appBuilder.packageName, 'zip', appBuilder.packageName)
