pkg_origin=brighthive
pkg_name=tpot-airflow
pkg_version=0.1.0
pkg_licence=('MIT')
pkg_maintainer="jee@brighthive.io, aretha@brighthive.io, stanley@brighthive.io"
pkg_filename=${pkg_name}-${pkg_version}.tar.gz
pkg_upstream_url="https://github.com/workforce-data-initiative/tpot-airflow.git"
pkg_build_deps=(core/virtualenv core/gcc core/bash)
pkg_deps=(core/coreutils core/python core/shadow)
pkg_interpreters=(bin/python3)
pkg_exports=([port]=listening_port)
pkg_exposes=(port)

pkg_lib_dirs=(lib)
pkg_include_dirs=(include)
pkg_bin_dirs=(bin)

pkg_svc_user=root
pkg_svc_group=root


do_unpack() {
  # create a env variable for the project root
  PROJECT_ROOT="${PLAN_CONTEXT}/.."

  mkdir -p $pkg_prefix
  # copy the contents of the source directory to the habitat cache path
  build_line "Copying project data to $pkg_prefix ..."
  cp -vr $PROJECT_ROOT/dags $pkg_prefix/
  cp -vr $PROJECT_ROOT/*.py $pkg_prefix/
  cp -vr $PROJECT_ROOT/setup.sh $pkg_prefix/
  cp -vr $PROJECT_ROOT/habitat $pkg_prefix/
  cp -vr $PROJECT_ROOT/requirements.txt $pkg_prefix/

}

do_build() {
  build_line "Exporting python path and airflow home to callable script"

  _runtime_python_path="$(pkg_path_for core/python)"
  # add the python path to a file to be sourced later.
  # (Do not indent export statements and the ENVS after them. If you do, cat will fail)
  cat > ./habitat/runtime_environment.sh << ENVS
export PYTHON_PATH="${_runtime_python_path}"
export AIRFLOW_HOME="$pkg_svc_var_path"
ENVS

}

do_install() {
  cd $pkg_prefix
  build_line "Creating virtual environment..."
  virtualenv "venv" -p python3
  . venv/bin/activate

  build_line "Installing requirements from requirements.txt ..."
  pip install -r requirements.txt
  build_line "Symbolic linking env file..."
  ln -fs {{pkg.path}}/habitat/runtime_environment.sh  {{pkg.svc_var_path}}
}
