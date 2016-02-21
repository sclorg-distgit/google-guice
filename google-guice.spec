%global pkg_name google-guice
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%if 0%{?fedora}
%bcond_without extensions
%endif

%global short_name guice

Name:           %{?scl_prefix}%{pkg_name}
Version:        3.1.3
Release:        9.13%{?dist}
Summary:        Lightweight dependency injection framework for Java 5 and above
License:        ASL 2.0
URL:            https://github.com/sonatype/sisu-%{short_name}
# ./create-tarball.sh %%{version}
Source0:        %{pkg_name}-%{version}.tar.xz
Source1:        create-tarball.sh
BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}maven-local >= 3.2.4-2
BuildRequires:  %{?scl_prefix}maven-remote-resources-plugin
BuildRequires:  %{?scl_prefix}munge-maven-plugin
BuildRequires:  %{?scl_prefix}apache-resource-bundles
BuildRequires:  %{?scl_prefix}aopalliance
BuildRequires:  %{?scl_prefix_java_common}atinject
BuildRequires:  %{?scl_prefix}cglib
BuildRequires:  %{?scl_prefix_java_common}guava
BuildRequires:  %{?scl_prefix_java_common}slf4j-api

%if %{with extensions}
buildrequires:  %{?scl_prefix}hibernate-jpa-2.0-api
BuildRequires:  %{?scl_prefix}springframework-beans
BuildRequires:  %{?scl_prefix_java_common}tomcat-servlet-3.0-api
%endif

# Test dependencies:
%if 0
BuildRequires:  %{?scl_prefix}maven-surefire-provider-testng
BuildRequires:  %{?scl_prefix}aqute-bnd
BuildRequires:  %{?scl_prefix_java_common}atinject-tck
BuildRequires:  %{?scl_prefix_java_common}easymock2
BuildRequires:  %{?scl_prefix_java_common}felix-framework
BuildRequires:  %{?scl_prefix}hibernate3-entitymanager
BuildRequires:  %{?scl_prefix}mvn(org.hsqldb:hsqldb-j5)
BuildRequires:  %{?scl_prefix}testng
BuildRequires:  %{?scl_prefix_java_common}slf4j-simple
%endif


%description
Put simply, Guice alleviates the need for factories and the use of new
in your Java code. Think of Guice's @Inject as the new new. You will
still need to write factories in some cases, but your code will not
depend directly on them. Your code will be easier to change, unit test
and reuse in other contexts.

Guice embraces Java's type safe nature, especially when it comes to
features introduced in Java 5 such as generics and annotations. You
might think of Guice as filling in missing features for core
Java. Ideally, the language itself would provide most of the same
features, but until such a language comes along, we have Guice.

Guice helps you design better APIs, and the Guice API itself sets a
good example. Guice is not a kitchen sink. We justify each feature
with at least three use cases. When in doubt, we leave it out. We
build general functionality which enables you to extend Guice rather
than adding every feature to the core framework.

%package -n %{?scl_prefix}%{short_name}-parent
Summary:        Guice parent POM

%description -n %{?scl_prefix}%{short_name}-parent
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides parent POM for Guice modules.

%if %{with extensions}

%package -n %{?scl_prefix}%{short_name}-assistedinject
Summary:        AssistedInject extension module for Guice

%description -n %{?scl_prefix}%{short_name}-assistedinject
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides AssistedInject module for Guice.

%package -n %{?scl_prefix}%{short_name}-extensions
Summary:        Extensions for Guice

%description -n %{?scl_prefix}%{short_name}-extensions
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides extensions POM for Guice.

%package -n %{?scl_prefix}%{short_name}-grapher
Summary:        Grapher extension module for Guice

%description -n %{?scl_prefix}%{short_name}-grapher
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Grapher module for Guice.

%package -n %{?scl_prefix}%{short_name}-jmx
Summary:        JMX extension module for Guice

%description -n %{?scl_prefix}%{short_name}-jmx
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides JMX module for Guice.

%package -n %{?scl_prefix}%{short_name}-jndi
Summary:        JNDI extension module for Guice

%description -n %{?scl_prefix}%{short_name}-jndi
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides JNDI module for Guice.

%package -n %{?scl_prefix}%{short_name}-multibindings
Summary:        MultiBindings extension module for Guice

%description -n %{?scl_prefix}%{short_name}-multibindings
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides MultiBindings module for Guice.

%package -n %{?scl_prefix}%{short_name}-persist
Summary:        Persist extension module for Guice

%description -n %{?scl_prefix}%{short_name}-persist
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Persist module for Guice.

%package -n %{?scl_prefix}%{short_name}-servlet
Summary:        Servlet extension module for Guice

%description -n %{?scl_prefix}%{short_name}-servlet
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Servlet module for Guice.

%package -n %{?scl_prefix}%{short_name}-spring
Summary:        Spring extension module for Guice

%description -n %{?scl_prefix}%{short_name}-spring
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Spring module for Guice.

%package -n %{?scl_prefix}%{short_name}-throwingproviders
Summary:        ThrowingProviders extension module for Guice

%description -n %{?scl_prefix}%{short_name}-throwingproviders
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides ThrowingProviders module for Guice.

%endif # with extensions

%package javadoc
Summary:        API documentation for Guice

%description javadoc
This package provides %{summary}.


%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

# We don't have struts2 in Fedora yet.
%pom_disable_module struts2 extensions

# Remove additional build profiles, which we don't use anyways
# and which are only pulling additional dependencies.
%pom_xpath_remove "pom:profile[pom:id='guice.with.jarjar']" core

# Animal sniffer is only causing problems. Disable it for now.
%pom_remove_plugin :animal-sniffer-maven-plugin core
%pom_remove_plugin :animal-sniffer-maven-plugin extensions

# We don't have the custom doclet used by upstream. Remove
# maven-javadoc-plugin to generate javadocs with default style.
%pom_remove_plugin :maven-javadoc-plugin

%pom_remove_dep javax.persistence:persistence-api extensions/persist
%pom_add_dep org.hibernate.javax.persistence:hibernate-jpa-2.0-api extensions/persist

# remove test dependency to make sure we don't produce requires
# see #1007498
%pom_xpath_remove "pom:dependency[pom:classifier[text()='tests']]" extensions

# Don't try to build extension modules unless they are needed
%if %{without extensions}
%pom_disable_module extensions
%endif

# Upstream doesn't generate pom.properties, but we need it.
sed -i "/<addMavenDescriptor>/d" pom.xml
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%if %{with extensions}
%mvn_alias ":guice-{assistedinject,grapher,jmx,jndi,multibindings,persist,\
servlet,spring,throwingproviders}" "com.google.inject.extensions:guice-@1"
%endif # with extensions

%mvn_package :::no_aop: sisu-guice

%mvn_file  ":guice-{*}"  %{short_name}/guice-@1
%mvn_file  ":sisu-guice" %{short_name}/%{pkg_name} %{pkg_name}
%mvn_alias ":sisu-guice" "com.google.inject:guice"
# Skip tests because of missing dependency (hsqldb-j5).
%mvn_build -f -s
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles-sisu-guice
%dir %{_mavenpomdir}/%{short_name}
%dir %{_javadir}/%{short_name}

%files -n %{?scl_prefix}%{short_name}-parent -f .mfiles-guice-parent
%doc COPYING

%if %{with extensions}
%files -n %{?scl_prefix}%{short_name}-assistedinject -f .mfiles-guice-assistedinject
%files -n %{?scl_prefix}%{short_name}-extensions -f .mfiles-guice-extensions
%files -n %{?scl_prefix}%{short_name}-grapher -f .mfiles-guice-grapher
%files -n %{?scl_prefix}%{short_name}-jmx -f .mfiles-guice-jmx
%files -n %{?scl_prefix}%{short_name}-jndi -f .mfiles-guice-jndi
%files -n %{?scl_prefix}%{short_name}-multibindings -f .mfiles-guice-multibindings
%files -n %{?scl_prefix}%{short_name}-persist -f .mfiles-guice-persist
%files -n %{?scl_prefix}%{short_name}-servlet -f .mfiles-guice-servlet
%files -n %{?scl_prefix}%{short_name}-spring -f .mfiles-guice-spring
%files -n %{?scl_prefix}%{short_name}-throwingproviders -f .mfiles-guice-throwingproviders
%endif # with extensions

%files javadoc -f .mfiles-javadoc
%doc COPYING


%changelog
* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 3.1.3-9.13
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 3.1.3-9.12
- maven33 rebuild

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-9.11
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 3.1.3-9.10
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 3.1.3-9.9
- Rebuild to regenerate requires from java-common

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 3.1.3-9.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-9.7
- Mass rebuild 2014-05-26

* Fri Feb 28 2014 Michael Simacek <msimacek@redhat.com> - 3.1.3-9.6
- Update slf4j BR

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-9.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-9.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 3.1.3-9.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-9.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-9.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.1.3-9
- Mass rebuild 2013-12-27

* Wed Sep 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-8
- Install no_aop artifact after javapackages update

* Thu Sep 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.3-7
- Remove dependency on tests from runtime
- Rel: rhbz#1007498

* Tue Sep 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-6
- Install no_aop artifact
- Res: rhbz#1006491

* Wed Sep  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-5
- Enable pom.properties
- Res: rhbz#1004360

* Wed Aug 07 2013 Michal Srb <msrb@redhat.com> - 3.1.3-4
- Add create-tarball.sh script to SRPM

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Michal Srb <msrb@redhat.com> - 3.1.3-4
- Add create-tarball.sh script to SRPM

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-3
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Apr 24 2013 Michal Srb <msrb@redhat.com> - 3.1.3-2
- Revert update to 3.1.4 (uses asm4)

* Thu Mar 14 2013 Michal Srb <msrb@redhat.com> - 3.1.3-1
- Update to upstream version 3.1.3
- Remove bundled JARs from tarball

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.1.2-11
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 31 2013 Michal Srb <msrb@redhat.com> - 3.1.2-10
- Remove all requires
- Correct usage of xmvn's macros

* Mon Jan 28 2013 Michal Srb <msrb@redhat.com> - 3.1.2-9
- Build with xmvn

* Fri Nov 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-8
- Remove README

* Fri Nov 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-7
- Repackage tarball

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-6
- Don't try to build extension modules unless they are needed

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-5
- Conditionalize %%install section too

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-4
- Conditionally disable extensions

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-3
- Update to new add_maven_depmap macro

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.2-2
- Use new generated maven filelist feature from javapackages-tools

* Fri Oct  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-1
- Complete rewrite of the spec file
- New upstream, to ease future maintenance
- Build with maven instead of ant
- Split into multiple subpackages

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.7.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb  9 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.6.rc2
- Temporary fix for maven buildroots

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.5.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.4.rc2
- Build with aqute-bnd (#745176)
- Use new maven macros
- Few packaging tweaks

* Tue May 24 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.3.rc2
- Add cglib and atinject to R

* Thu May 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.2.rc2
- Remove test and missing deps from pom.xml

* Tue Mar  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.1.rc2
- Update to 3.0rc2
- Changes according to new guidelines (versionless jars & javadocs)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4.1219svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-3.1219svn
- Add java-devel >= 1:1.6.0 to BR

* Wed Oct 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-2.1219svn
- Moved munge repacking to prep
- Added -Dversion to change generated manifest version
- Removed http part of URL

* Thu Oct  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-1.1219svn
- Initial version of the package
