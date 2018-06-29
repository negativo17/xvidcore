Name:           xvidcore
Version:        1.3.5
Release:        1%{?dist}
Summary:        MPEG-4 Simple and Advanced Simple Profile codec
License:        GPLv2+
URL:            http://www.xvid.org/

Source0:        http://downloads.xvid.org/downloads/%{name}-%{version}.tar.bz2

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

%ifarch %{ix86} x86_64
BuildRequires:  nasm >= 2.0
%endif

%description
The Xvid video codec implements MPEG-4 Simple Profile and Advanced Simple
Profile standards. It permits compressing and decompressing digital video in
order to reduce the required bandwidth of video data for transmission over
computer networks or efficient storage on CDs or DVDs. Due to its unrivaled
quality Xvid has gained great popularity and is used in many other GPLed
applications, like e.g. Transcode, MEncoder, MPlayer, Xine and many more.

%package        devel
Summary:        Development files for the Xvid video codec
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains header files, static library and API documentation for the
Xvid video codec.

%prep
export RPM_LD_FLAGS="%{?__global_ldflags} -fPIC"
%autosetup -n %{name}
sed -i -e 's|644 $(BUILD_DIR)/$(SHARED_LIB) |755 $(BUILD_DIR)/$(SHARED_LIB) |g' \
    build/generic/Makefile

for file in AUTHORS ChangeLog; do
    iconv -f iso-8859-1 -t utf-8 -o $file.utf8 $file
    touch -r $file $file.utf8
    mv $file.utf8 $file
done

%build
cd build/generic
autoreconf -vif
%configure --disable-static
%make_build
cd -

%install
make -C build/generic install DESTDIR=%{buildroot}
find %{buildroot} -name "*.a" -delete

%ldconfig_scriptlets

%files
%license LICENSE
%doc README AUTHORS ChangeLog
%{_libdir}/libxvidcore.so.*

%files devel
%doc CodingStyle TODO examples/
%{_includedir}/xvid.h
%{_libdir}/libxvidcore.so

%changelog
* Fri Jun 29 2018 Simone Caronni <negativo17@gmail.com> - 1.3.5-1
- Update to 1.3.5.
- Clean up SPEC file.

* Fri Apr 22 2016 Simone Caronni <negativo17@gmail.com> - 1.3.4-3
- Update SPEC file.
- Trim changelog.
- Use autotools instead of Makefile.

* Sun Oct 25 2015 Dominik Mierzejewski <rpm at greysector.net> - 1.3.4-2
- using ldconfig to generate correct so filename is no longer needed
