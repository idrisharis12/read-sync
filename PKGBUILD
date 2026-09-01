pkgname=read-sync
pkgver=0.1.11
pkgrel=1
pkgdesc="Terminal native manga and comic reader with tracker sync and headless server."
arch=('any')
url="https://github.com/blakie/read-sync"
license=('MIT')
depends=('python' 'python-requests' 'python-tqdm' 'python-pillow' 'python-textual' 'python-fastapi' 'python-uvicorn')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
  cd "$pkgname-$pkgver"
  python setup.py build
}

package() {
  cd "$pkgname-$pkgver"
  python setup.py install --root="$pkgdir" --optimize=1
}
