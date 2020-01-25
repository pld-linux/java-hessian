

%define		srcname	hessian
Summary:	hessian binary web service protocol
Name:		java-hessian
Version:	3.2.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://hessian.caucho.com/download/hessian-%{version}-src.jar
# Source0-md5:	da84b17bc21deb9a152cce2a9d1429b7
Patch0:		%{name}-libgcj.patch
URL:		http://hessian.caucho.com/
BuildRequires:	java-commons-httpclient
BuildRequires:	java-gcj-compat-devel
BuildRequires:	java-servletapi5
Requires:	java-commons-httpclient
Requires:	java-servletapi5
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Hessian binary web service protocol makes web services usable
without requiring a large framework, and without learning yet another
alphabet soup of protocols. Because it is a binary protocol, it is
well-suited to sending binary data without any need to extend the
protocol with attachments.

%package javadoc
Summary:	Online manual for java-hessian
Summary(pl.UTF-8):	Dokumentacja online do java-hessian
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for java-hessian.

%description javadoc -l pl.UTF-8
Dokumentacja do java-hessian.

%description javadoc -l fr.UTF-8
Javadoc pour java-hessian.

%prep
%setup -qc

%patch0 -p1

%build
required_jars="commons-httpclient servlet"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

%javac \
	-classpath $CLASSPATH \
	-source 1.5 \
	-target 1.5 \
	-d build \
	$(find -name '*.java')

%javadoc -all -d apidocs
%jar -cf %{srcname}-%{version}.jar -C build com

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

cp -a %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a target/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
