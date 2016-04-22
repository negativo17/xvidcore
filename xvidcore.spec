Name:           xvidcore
Version:        1.3.4
Release:        3%{?dist}
Summary:        MPEG-4 Simple and Advanced Simple Profile codec
License:        GPLv2+
URL:            http://www.xvid.org/

Source0:        http://downloads.xvid.org/downloads/%{name}-%{version}.tar.bz2

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  perl

%ifarch %{ix86} x86_64
BuildRequires:  nasm >= 2.0
%endif

%description
The Xvid video codec implements MPEG-4 Simple Profile and Advanced Simple
Profile standards. It permits compressing and decompressing digital video in
order to reduce the required bandwidth of video data for transmission over
computer networks or efficient storage on CDs or DVDs. Due to its unrivalled
quality Xvid has gained great popularity and is used in many other GPLed
applications, like e.g. Transcode, MEncoder, MPlayer, Xine and many more.

%package        devel
Summary:        Development files for the Xvid video codec
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains header files, static library and API documentation for the
Xvid video codec.


%prep
%setup -q -n %{name}
sed -i -e 's|644 $(BUILD_DIR)/$(SHARED_LIB) |755 $(BUILD_DIR)/$(SHARED_LIB) |g' \
    build/generic/Makefile

for file in AUTHORS ChangeLog; do
    iconv -f iso-8859-1 -t utf-8 -o $file.utf8 $file
    touch -r $file $file.utf8
    mv $file.utf8 $file
done

# Yes, we want to see the build output.
perl -pi -e 's/^\t@(?!echo\b)/\t/' build/generic/Makefile


%build
cd build/generic
autoreconf -vif
%configure --disable-static
make %{?_smp_mflags} 
cd -


%install
make -C build/generic install DESTDIR=%{buildroot}
find %{buildroot} -name "*.a" -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README AUTHORS ChangeLog
%{_libdir}/libxvidcore.so.*

%files devel
%doc CodingStyle TODO examples/
%{_includedir}/xvid.h
%{_libdir}/libxvidcore.so

%changelog
* Fri Apr 22 2016 Simone Caronni <negativo17@gmail.com> - 1.3.4-3
- Update SPEC file.
- Trim changelog.
- Use autotools instead of Makefile.

* Sun Oct 25 2015 Dominik Mierzejewski <rpm at greysector.net> - 1.3.4-2
- using ldconfig to generate correct so filename is no longer needed
