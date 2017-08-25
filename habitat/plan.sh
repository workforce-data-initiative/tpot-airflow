pkg_origin=brighthive
pkg_name=tpot-airflow
pkg_version=0.1.0
pkg_licence=('MIT')
pkg_maintainer="jee@brighthive.io, aretha@brighthive.io, stanley@brighthive.io"
pkg_filename=${pkg_name}-${pkg_version}.tar.gz
pkg_upstream_url="https://github.com/workforce-data-initiative/tpot-airflow.git"
pkg_build_deps=(core/virtualenv core/gcc)
pkg_deps=(core/bash core/coreutils core/python)
pkg_exports=([port]=listening_port)
pkg_exposes=(port)

do_verify () {
  return 0
}

do_clean() {
  return 0
}

do_unpack() {
  # create a env variable for the project root
  PROJECT_ROOT="${PLAN_CONTEXT}/.."

  mkdir -p $pkg_prefix
  # copy the contents of the source directory to the habitat cache path
  build_line "Copying project data to $pkg_prefix ..."
  cp -r $PROJECT_ROOT/dags $pkg_prefix/
  cp -r $PROJECT_ROOT/*.py $pkg_prefix/
  cp -r $PROJECT_ROOT/requirements.txt $pkg_prefix/
  cp -r $PROJECT_ROOT/setup.sh $pkg_prefix/
}

do_build() {
  return 0
}

do_install() {
  cd $pkg_prefix
  build_line "Creating a virtual environment ..."
  virtualenv venv -p python3
  source venv/bin/activate
  build_line "Installing requirements from requirements.txt ..."
  pip install -r requirements.txt
}
