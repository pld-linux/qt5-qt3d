#
# Conditional build:
%bcond_without	qch	# documentation in QCH format

%define		orgname		qt3d
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 3D libraries
Summary(pl.UTF-8):	Biblioteki Qt5 3D
Name:		qt5-%{orgname}
Version:	5.5.1
Release:	1
License:	LGPL v3 or GPL v2+ or commercial
Group:		X11/Libraries
Source0:	http://download.qt.io/official_releases/qt/5.5/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	872dfbe166154c2e0e89317ab23d2cd6
URL:		http://www.qt.io/
BuildRequires:	Qt5Concurrent-devel >= %{qtbase_ver}
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5OpenGL-devel >= %{qtbase_ver}
BuildRequires:	Qt5OpenGLExtensions-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	assimp-devel
BuildRequires:	pkgconfig
%if %{with qch}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 3D libraries.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera biblioteki Qt5 3D.

%package -n Qt53D
Summary:	The Qt5 3D libraries
Summary(pl.UTF-8):	Biblioteki Qt5 3D
Group:		X11/Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Gui >= %{qtbase_ver}

%description -n Qt53D
Qt5 3D libraries.
platform.

%description -n Qt53D -l pl.UTF-8
Biblioteki Qt5 3D.

%package -n Qt53D-devel
Summary:	Qt5 3D - development files
Summary(pl.UTF-8):	Biblioteki Qt5 3D - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt53D = %{version}-%{release}
Requires:	Qt5Concurrent-devel >= %{qtbase_ver}
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Gui-devel >= %{qtbase_ver}
Requires:	Qt5Qml-devel >= %{qtbase_ver}

%description -n Qt53D-devel
Qt5 3D - development files.

%description -n Qt53D-devel -l pl.UTF-8
Biblioteki Qt5 3D - pliki programistyczne.

%package doc
Summary:	Qt5 3D documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 3D w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 3D documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 3D w formacie HTML.

%package doc-qch
Summary:	Qt5 3D documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 3D w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
Qt5 3D documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 3D w formacie QCH.

%package examples
Summary:	Qt5 3D examples
Summary(pl.UTF-8):	Przykłady do bibliotek Qt5 3D
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Qt5 3D examples.

%description examples -l pl.UTF-8
Przykłady do bibliotek Qt5 3D.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%build
qmake-qt5
%{__make}
%{__make} %{!?with_qch:html_}docs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_%{!?with_qch:html_}docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.?
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/qt3d

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt53D -p /sbin/ldconfig
%postun	-n Qt53D -p /sbin/ldconfig

%files -n Qt53D
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libQt53DCollision.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DCollision.so.5
%attr(755,root,root) %{_libdir}/libQt53DCore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DCore.so.5
%attr(755,root,root) %{_libdir}/libQt53DInput.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DInput.so.5
%attr(755,root,root) %{_libdir}/libQt53DLogic.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DLogic.so.5
%attr(755,root,root) %{_libdir}/libQt53DQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DQuick.so.5
%attr(755,root,root) %{_libdir}/libQt53DQuickRenderer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DQuickRenderer.so.5
%attr(755,root,root) %{_libdir}/libQt53DRenderer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DRenderer.so.5
# loaded from src/render/backend/renderer.cpp
%dir %{qt5dir}/plugins/sceneparsers
%attr(755,root,root) %{qt5dir}/plugins/sceneparsers/libassimpsceneparser.so
%attr(755,root,root) %{qt5dir}/plugins/sceneparsers/libgltfsceneparser.so
%dir %{qt5dir}/qml/Qt3D
%attr(755,root,root) %{qt5dir}/qml/Qt3D/libquick3dcoreplugin.so
%{qt5dir}/qml/Qt3D/qmldir
%dir %{qt5dir}/qml/Qt3D/Collision
%attr(755,root,root) %{qt5dir}/qml/Qt3D/Collision/libquick3dcollisionplugin.so
%{qt5dir}/qml/Qt3D/Collision/qmldir
%dir %{qt5dir}/qml/Qt3D/Input
%attr(755,root,root) %{qt5dir}/qml/Qt3D/Input/libquick3dinputplugin.so
%{qt5dir}/qml/Qt3D/Input/qmldir
%dir %{qt5dir}/qml/Qt3D/Logic
%attr(755,root,root) %{qt5dir}/qml/Qt3D/Logic/libquick3dlogicplugin.so
%{qt5dir}/qml/Qt3D/Logic/qmldir
%dir %{qt5dir}/qml/Qt3D/Renderer
%attr(755,root,root) %{qt5dir}/qml/Qt3D/Renderer/libquick3drendererplugin.so
%{qt5dir}/qml/Qt3D/Renderer/qmldir
%dir %{qt5dir}/qml/QtQuick/Scene3D
%attr(755,root,root) %{qt5dir}/qml/QtQuick/Scene3D/libqtquickscene3dplugin.so
%{qt5dir}/qml/QtQuick/Scene3D/qmldir

%files -n Qt53D-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt53DCollision.so
%attr(755,root,root) %{_libdir}/libQt53DCore.so
%attr(755,root,root) %{_libdir}/libQt53DInput.so
%attr(755,root,root) %{_libdir}/libQt53DLogic.so
%attr(755,root,root) %{_libdir}/libQt53DQuick.so
%attr(755,root,root) %{_libdir}/libQt53DQuickRenderer.so
%attr(755,root,root) %{_libdir}/libQt53DRenderer.so
%{_libdir}/libQt53DCollision.prl
%{_libdir}/libQt53DCore.prl
%{_libdir}/libQt53DInput.prl
%{_libdir}/libQt53DLogic.prl
%{_libdir}/libQt53DQuick.prl
%{_libdir}/libQt53DQuickRenderer.prl
%{_libdir}/libQt53DRenderer.prl
%{_includedir}/qt5/Qt3DCollision
%{_includedir}/qt5/Qt3DCore
%{_includedir}/qt5/Qt3DInput
%{_includedir}/qt5/Qt3DLogic
%{_includedir}/qt5/Qt3DQuick
%{_includedir}/qt5/Qt3DQuickRenderer
%{_includedir}/qt5/Qt3DRenderer
%{_pkgconfigdir}/Qt53DCollision.pc
%{_pkgconfigdir}/Qt53DCore.pc
%{_pkgconfigdir}/Qt53DInput.pc
%{_pkgconfigdir}/Qt53DLogic.pc
%{_pkgconfigdir}/Qt53DQuick.pc
%{_pkgconfigdir}/Qt53DQuickRenderer.pc
%{_pkgconfigdir}/Qt53DRenderer.pc
%{_libdir}/cmake/Qt53DCollision
%{_libdir}/cmake/Qt53DCore
%{_libdir}/cmake/Qt53DInput
%{_libdir}/cmake/Qt53DLogic
%{_libdir}/cmake/Qt53DQuick
%{_libdir}/cmake/Qt53DQuickRenderer
%{_libdir}/cmake/Qt53DRenderer
%{qt5dir}/mkspecs/modules/qt_lib_3dcollision.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dcollision_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dcore.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dcore_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dinput.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dinput_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dlogic.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dlogic_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquick.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquick_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickrenderer.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickrenderer_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3drenderer.pri
%{qt5dir}/mkspecs/modules/qt_lib_3drenderer_private.pri

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qt3dcollision
%{_docdir}/qt5-doc/qt3dcore
%{_docdir}/qt5-doc/qt3dlogic
%{_docdir}/qt5-doc/qt3drenderer

%if %{with qch}
%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qt3dcollision.qch
%{_docdir}/qt5-doc/qt3dcore.qch
%{_docdir}/qt5-doc/qt3dlogic.qch
%{_docdir}/qt5-doc/qt3drenderer.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
