#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qt3d
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 3D libraries
Summary(pl.UTF-8):	Biblioteki Qt5 3D
Name:		qt5-%{orgname}
Version:	5.15.0
Release:	1
License:	LGPL v3 or GPL v2+ or commercial
Group:		X11/Libraries
Source0:	http://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-src-%{version}.tar.xz
# Source0-md5:	7f8a281467f80dbd94eb9406e2e7e671
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
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
BuildRequires:	qt5-doc-common >= %{qttools_ver}
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
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
qmake-qt5
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
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
%attr(755,root,root) %{_libdir}/libQt53DAnimation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DAnimation.so.5
%attr(755,root,root) %{_libdir}/libQt53DCore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DCore.so.5
%attr(755,root,root) %{_libdir}/libQt53DExtras.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DExtras.so.5
%attr(755,root,root) %{_libdir}/libQt53DInput.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DInput.so.5
%attr(755,root,root) %{_libdir}/libQt53DLogic.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DLogic.so.5
%attr(755,root,root) %{_libdir}/libQt53DQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DQuick.so.5
%attr(755,root,root) %{_libdir}/libQt53DQuickAnimation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DQuickAnimation.so.5
%attr(755,root,root) %{_libdir}/libQt53DQuickExtras.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DQuickExtras.so.5
%attr(755,root,root) %{_libdir}/libQt53DQuickInput.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DQuickInput.so.5
%attr(755,root,root) %{_libdir}/libQt53DQuickRender.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DQuickRender.so.5
%attr(755,root,root) %{_libdir}/libQt53DRender.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DRender.so.5
%attr(755,root,root) %{_libdir}/libQt53DQuickScene2D.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt53DQuickScene2D.so.5
# loaded from src/render/backend/renderer.cpp
%dir %{qt5dir}/plugins/geometryloaders
%attr(755,root,root) %{_libdir}/qt5/plugins/geometryloaders/libdefaultgeometryloader.so
%attr(755,root,root) %{_libdir}/qt5/plugins/geometryloaders/libgltfgeometryloader.so
%dir %{qt5dir}/plugins/renderers
%{qt5dir}/plugins/renderers/libopenglrenderer.so
%dir %{qt5dir}/plugins/renderplugins
%attr(755,root,root) %{_libdir}/qt5/plugins/renderplugins/libscene2d.so
%dir %{qt5dir}/plugins/sceneparsers
%attr(755,root,root) %{_libdir}/qt5/plugins/sceneparsers/libassimpsceneimport.so
%attr(755,root,root) %{_libdir}/qt5/plugins/sceneparsers/libgltfsceneexport.so
%attr(755,root,root) %{_libdir}/qt5/plugins/sceneparsers/libgltfsceneimport.so
%dir %{qt5dir}/qml/Qt3D
%dir %{qt5dir}/qml/Qt3D/Animation
%attr(755,root,root) %{qt5dir}/qml/Qt3D/Animation/libquick3danimationplugin.so
%{qt5dir}/qml/Qt3D/Animation/plugins.qmltypes
%{qt5dir}/qml/Qt3D/Animation/qmldir
%dir %{qt5dir}/qml/Qt3D/Input
%attr(755,root,root) %{qt5dir}/qml/Qt3D/Input/libquick3dinputplugin.so
%{qt5dir}/qml/Qt3D/Input/plugins.qmltypes
%{qt5dir}/qml/Qt3D/Input/qmldir
%dir %{qt5dir}/qml/Qt3D/Logic
%attr(755,root,root) %{qt5dir}/qml/Qt3D/Logic/libquick3dlogicplugin.so
%{qt5dir}/qml/Qt3D/Logic/plugins.qmltypes
%{qt5dir}/qml/Qt3D/Logic/qmldir
%dir %{qt5dir}/qml/QtQuick/Scene2D
%attr(755,root,root) %{qt5dir}/qml/QtQuick/Scene2D/libqtquickscene2dplugin.so
%{qt5dir}/qml/QtQuick/Scene2D/plugins.qmltypes
%{qt5dir}/qml/QtQuick/Scene2D/qmldir
%dir %{qt5dir}/qml/QtQuick/Scene3D
%attr(755,root,root) %{qt5dir}/qml/QtQuick/Scene3D/libqtquickscene3dplugin.so
%{qt5dir}/qml/QtQuick/Scene3D/plugins.qmltypes
%{qt5dir}/qml/QtQuick/Scene3D/qmldir
%dir %{qt5dir}/qml/Qt3D/Core
%attr(755,root,root) %{qt5dir}/qml/Qt3D/Core/libquick3dcoreplugin.so
%{qt5dir}/qml/Qt3D/Core/plugins.qmltypes
%{qt5dir}/qml/Qt3D/Core/qmldir
%dir %{qt5dir}/qml/Qt3D/Extras
%attr(755,root,root) %{qt5dir}/qml/Qt3D/Extras/libquick3dextrasplugin.so
%{qt5dir}/qml/Qt3D/Extras/plugins.qmltypes
%{qt5dir}/qml/Qt3D/Extras/qmldir
%dir %{qt5dir}/qml/Qt3D/Render
%attr(755,root,root) %{qt5dir}/qml/Qt3D/Render/libquick3drenderplugin.so
%{qt5dir}/qml/Qt3D/Render/plugins.qmltypes
%{qt5dir}/qml/Qt3D/Render/qmldir

%files -n Qt53D-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{qt5dir}/bin/qgltf
%attr(755,root,root) %{_libdir}/libQt53DAnimation.so
%attr(755,root,root) %{_libdir}/libQt53DCore.so
%attr(755,root,root) %{_libdir}/libQt53DExtras.so
%attr(755,root,root) %{_libdir}/libQt53DInput.so
%attr(755,root,root) %{_libdir}/libQt53DLogic.so
%attr(755,root,root) %{_libdir}/libQt53DQuickAnimation.so
%attr(755,root,root) %{_libdir}/libQt53DQuickExtras.so
%attr(755,root,root) %{_libdir}/libQt53DQuickInput.so
%attr(755,root,root) %{_libdir}/libQt53DQuickRender.so
%attr(755,root,root) %{_libdir}/libQt53DQuickScene2D.so
%attr(755,root,root) %{_libdir}/libQt53DQuick.so
%attr(755,root,root) %{_libdir}/libQt53DRender.so
%{_libdir}/libQt53DAnimation.prl
%{_libdir}/libQt53DCore.prl
%{_libdir}/libQt53DExtras.prl
%{_libdir}/libQt53DInput.prl
%{_libdir}/libQt53DLogic.prl
%{_libdir}/libQt53DQuickAnimation.prl
%{_libdir}/libQt53DQuickExtras.prl
%{_libdir}/libQt53DQuickInput.prl
%{_libdir}/libQt53DQuick.prl
%{_libdir}/libQt53DQuickRender.prl
%{_libdir}/libQt53DQuickScene2D.prl
%{_libdir}/libQt53DRender.prl
%{_includedir}/qt5/Qt3DAnimation
%{_includedir}/qt5/Qt3DCore
%{_includedir}/qt5/Qt3DExtras
%{_includedir}/qt5/Qt3DInput
%{_includedir}/qt5/Qt3DLogic
%{_includedir}/qt5/Qt3DQuick
%{_includedir}/qt5/Qt3DQuickAnimation
%{_includedir}/qt5/Qt3DQuickExtras
%{_includedir}/qt5/Qt3DQuickInput
%{_includedir}/qt5/Qt3DQuickRender
%{_includedir}/qt5/Qt3DQuickScene2D
%{_includedir}/qt5/Qt3DRender
%{_pkgconfigdir}/Qt53DAnimation.pc
%{_pkgconfigdir}/Qt53DCore.pc
%{_pkgconfigdir}/Qt53DExtras.pc
%{_pkgconfigdir}/Qt53DInput.pc
%{_pkgconfigdir}/Qt53DLogic.pc
%{_pkgconfigdir}/Qt53DQuickAnimation.pc
%{_pkgconfigdir}/Qt53DQuickExtras.pc
%{_pkgconfigdir}/Qt53DQuickInput.pc
%{_pkgconfigdir}/Qt53DQuick.pc
%{_pkgconfigdir}/Qt53DQuickRender.pc
%{_pkgconfigdir}/Qt53DQuickScene2D.pc
%{_pkgconfigdir}/Qt53DRender.pc
%{_libdir}/cmake/Qt53DAnimation
%{_libdir}/cmake/Qt53DCore
%{_libdir}/cmake/Qt53DExtras
%{_libdir}/cmake/Qt53DInput
%{_libdir}/cmake/Qt53DLogic
%{_libdir}/cmake/Qt53DQuick
%{_libdir}/cmake/Qt53DQuickAnimation
%{_libdir}/cmake/Qt53DQuickExtras
%{_libdir}/cmake/Qt53DQuickInput
%{_libdir}/cmake/Qt53DQuickRender
%{_libdir}/cmake/Qt53DQuickScene2D
%{_libdir}/cmake/Qt53DRender

%{qt5dir}/mkspecs/modules/qt_lib_3danimation.pri
%{qt5dir}/mkspecs/modules/qt_lib_3danimation_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dcore.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dcore_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dextras.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dextras_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dinput.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dinput_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dlogic.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dlogic_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickanimation.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickanimation_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickextras.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickextras_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickinput.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickinput_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquick.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquick_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickrender.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickrender_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickscene2d.pri
%{qt5dir}/mkspecs/modules/qt_lib_3dquickscene2d_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_3drender.pri
%{qt5dir}/mkspecs/modules/qt_lib_3drender_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qt3d

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qt3d.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
