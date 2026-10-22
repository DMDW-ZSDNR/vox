# AO groupe - design system preview

A standalone Flutter 3 / Material 3 preview of the AO groupe design system.
The showcase is the app's entry screen; it is not a splash, onboarding, or
production home screen.

## Run

From this directory, with Flutter 3 installed:

```powershell
flutter pub get
flutter run -d chrome
```

Arabic is the default locale and uses right-to-left layout. Use the language
selector to preview French and English, and the theme selector to switch
between light, dark, and system appearance.

## Verify and build for web

```powershell
dart format --output=none --set-exit-if-changed lib test
flutter analyze --fatal-infos
flutter test
flutter build web --release
```

The static web build is written to `build/web/`. Deploy that directory to a
static host with single-page-app fallback routing enabled. A GitHub Actions
workflow runs formatting, analysis, widget tests, and the release web build
when this app changes.

This preview has no backend, external packages, or credentials. Its sample
product and price are illustrative; they are not live inventory or pricing.
