Summary:	Netbeans CVS module and library
Name:		javacvs
Version:	5.0
Release:	10
Group:		Development/Java
License:	Sun Public License
Url:		http://javacvs.netbeans.org/
Source0:	%{name}-%{version}.tar.gz
# cvs -d :pserver:anoncvs@cvs.netbeans.org:/cvs login
# cvs -d :pserver:anoncvs@cvs.netbeans.org:/cvs export -r release50-BLD200601252030 javacvs
Source1:	http://repo1.maven.org/maven2/org/netbeans/lib/cvsclient/20060125/cvsclient-20060125.pom
Source2:	javacvs-projectized.xml
# curl -o javacvs-projectized.xml 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/templates/projectized.xml?content-type=text%2Fplain&rev=1.61'
Source3:	javacvs-default.xml
# curl -o javacvs-default.xml 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/default.xml?content-type=text%2Fplain&rev=1.19'
Source4:	javacvs-default-properties.xml
# curl -o javacvs-default-properties.xml 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/default-properties.xml?content-type=text%2Fplain&rev=1.10'
Source5:	javacvs-common.xml
# curl -o javacvs-common.xml 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/templates/common.xml?content-type=text%2Fplain&rev=1.27.4.1'
Source6:	javacvs-javadoctools-template.xml
# curl -o javacvs-javadoctools-template.xml 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/javadoctools/template.xml?content-type=text%2Fplain&rev=1.59'
Source7:	javacvs-javadoctools-properties.xml
# curl -o javacvs-javadoctools-properties.xml 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/javadoctools/properties.xml?content-type=text%2Fplain&rev=1.16'
Source8:	javacvs-javadoctools-links.xml
# curl -o javacvs-javadoctools-links.xml 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/javadoctools/links.xml?content-type=text%2Fplain&rev=1.16'
Source9:	javacvs-javadoctools-replaces.xml
# curl -o javacvs-javadoctools-replaces.xml 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/javadoctools/replaces.xml?content-type=text%2Fplain&rev=1.17'
Source10:	javacvs-javadoctools-disallowed-links.xml
# curl -o javacvs-javadoctools-disallowed-links.xml 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/javadoctools/disallowed-links.xml?content-type=text%2Fplain&rev=1.4'
Source11:	javacvs-javadoctools-apichanges-empty.xml
# curl -o javacvs-javadoctools-apichanges-empty.xml 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/javadoctools/apichanges-empty.xml?content-type=text%2Fplain&rev=1.1'
Source12:	javacvs-javadoctools-apichanges.xsl
# curl -o javacvs-javadoctools-apichanges.xsl 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/javadoctools/apichanges.xsl?content-type=text%2Fplain&rev=1.8'
Source13:	javacvs-javadoctools-javadoc.css
# curl -o javacvs-javadoctools-javadoc.css 'http://nbbuild.netbeans.org/source/browse/*checkout*/nbbuild/javadoctools/javadoc.css?content-type=text%2Fplain&rev=1.4'
Patch0:		%{name}-libmodule-build.patch
BuildArch:	noarch

BuildRequires:	ant-nodeps
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:	jpackage-utils >= 0:1.7.4
Requires(post,postun):	jpackage-utils >= 0:1.7.4

%description
The module provides UI frontend to the CVS in the Netbeans 
IDE. Just now there is work in progress addressing project 
and typical workflow integration. 
Supported commands are:	commit, update, add, remove, tag, 
checkout, import, history, diff, status, log, annotate. 
The library implements a CVS client protocol in Java. It 
allows to access CVS servers without setting up an external 
cvs program. It's base for the module. 

%package        lib
Summary:	Netbeans %{name} library
Group:		Development/Java
Requires:	%{name} = %{EVRD}

%description    lib
%{summary}.

%package        lib-javadoc
Summary:	Javadoc for %{name} lib
Group:		Development/Java

%description    lib-javadoc
%{summary}.

%prep
%setup -qn %{name}
%remove_java_binaries
%patch0 -p0 -b .sav
mkdir -p libs/external
mkdir -p nbbuild/dummy
mkdir -p nbbuild/javadoctools
mkdir -p nbbuild/netbeans/
mkdir -p nbbuild/templates/
cp %{SOURCE2} nbbuild/templates/projectized.xml
cp %{SOURCE3} nbbuild/default.xml
cp %{SOURCE4} nbbuild/default-properties.xml
cp %{SOURCE5} nbbuild/templates/common.xml
cp %{SOURCE6} nbbuild/javadoctools/template.xml
cp %{SOURCE7} nbbuild/javadoctools/properties.xml
cp %{SOURCE8} nbbuild/javadoctools/links.xml
cp %{SOURCE9} nbbuild/javadoctools/replaces.xml
cp %{SOURCE10} nbbuild/javadoctools/disallowed-links.xml
cp %{SOURCE11} nbbuild/javadoctools/apichanges-empty.xml
cp %{SOURCE12} nbbuild/javadoctools/apichanges.xsl
cp %{SOURCE13} nbbuild/javadoctools/javadoc.css

%build
cd libmodule
export JAVA_HOME=%{_prefix}/lib/jvm/java-1.6.0
ant -Dcluster=netbeans -Dcode.name.base.dashes=cvsclient jar javadoc

%install
install -dm 755 %{buildroot}%{_javadir}/%{name}

install -pm 644 libmodule/netbeans/modules/cvsclient.jar \
	%{buildroot}%{_javadir}/%{name}/cvslib-%{version}.jar
ln -s cvslib-%{version}.jar \
	%{buildroot}%{_javadir}/%{name}/cvslib.jar
ln -s cvslib-%{version}.jar \
	%{buildroot}%{_javadir}/%{name}/cvsclient.jar
%add_to_maven_depmap org.netbeans lib %{version} JPP/%{name} cvslib
%add_to_maven_depmap org.netbeans.lib cvsclient %{version} JPP/%{name} cvsclient

# poms
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -m 644 %{SOURCE1} \
	%{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-cvslib.pom
install -m 644 %{SOURCE1} \
	%{buildroot}%{_datadir}/maven2/poms/JPP.%{name}-cvsclient.pom

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}-lib-%{version}
cp -pr nbbuild/build/javadoc/cvsclient/* %{buildroot}%{_javadocdir}/%{name}-lib-%{version}
ln -s %{name}-lib-%{version} %{buildroot}%{_javadocdir}/%{name}-lib 

%post lib
%update_maven_depmap

%postun lib
%update_maven_depmap

%files
%dir %{_javadir}/%{name}

%files lib
%{_javadir}/%{name}/*.jar
%{_datadir}/maven2/poms/*
%config(noreplace) %{_mavendepmapfragdir}/*

%files lib-javadoc
%doc %{_javadocdir}/%{name}-lib-%{version}
%doc %{_javadocdir}/%{name}-lib

