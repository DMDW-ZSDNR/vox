import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import 'l10n/app_localizations.dart';
import 'screens/design_system_showcase.dart';
import 'theme/app_theme.dart';

void main() {
  runApp(const AoGroupeApp());
}

class AoGroupeApp extends StatefulWidget {
  const AoGroupeApp({super.key});

  @override
  State<AoGroupeApp> createState() => _AoGroupeAppState();
}

class _AoGroupeAppState extends State<AoGroupeApp> {
  Locale _locale = const Locale('ar');
  ThemeMode _themeMode = ThemeMode.system;

  void _setLocale(Locale locale) {
    setState(() => _locale = locale);
  }

  void _setThemeMode(ThemeMode themeMode) {
    setState(() => _themeMode = themeMode);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AO groupe',
      debugShowCheckedModeBanner: false,
      locale: _locale,
      supportedLocales: AppLocalizations.supportedLocales,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      theme: AppTheme.light(),
      darkTheme: AppTheme.dark(),
      themeMode: _themeMode,
      home: DesignSystemShowcase(
        locale: _locale,
        themeMode: _themeMode,
        onLocaleChanged: _setLocale,
        onThemeModeChanged: _setThemeMode,
      ),
    );
  }
}
