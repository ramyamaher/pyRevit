﻿using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Text.RegularExpressions;
using System.Security.Principal;
using System.Text;

using pyRevitLabs.Common;
using pyRevitLabs.Common.Extensions;

using MadMilkman.Ini;
using pyRevitLabs.Json.Linq;
using pyRevitLabs.NLog;
using pyRevitLabs.TargetApps.Revit;

namespace pyRevitLabs.PyRevit {
    public static class PyRevitCaches {
        private static readonly Logger logger = LogManager.GetCurrentClassLogger();

        // pyrevit cache folder
        // @reviewed
        public static string GetCacheDirectory(int revitYear) {
            return Path.Combine(PyRevitLabsConsts.PyRevitPath, revitYear.ToString());
        }

        // clear cache
        // @handled @logs
        public static void ClearCache(int revitYear) {
            // make sure all revit instances are closed
            if (CommonUtils.VerifyPath(PyRevitLabsConsts.PyRevitPath)) {
                RevitController.KillRunningRevits(revitYear);
                CommonUtils.DeleteDirectory(GetCacheDirectory(revitYear));
            }
            else
                logger.Debug($"{PyRevitLabsConsts.PyRevitPath} directory not found, nothing to clear.");
        }

        // clear all caches
        // @handled @logs
        public static void ClearAllCaches() {
            var cacheDirFinder = new Regex(@"\d\d\d\d");
            if (CommonUtils.VerifyPath(PyRevitLabsConsts.PyRevitPath)) {
                foreach (string subDir in Directory.GetDirectories(PyRevitLabsConsts.PyRevitPath)) {
                    var dirName = Path.GetFileName(subDir);
                    if (cacheDirFinder.IsMatch(dirName))
                        ClearCache(int.Parse(dirName));
                }
            }
            else
                logger.Debug($"{PyRevitLabsConsts.PyRevitPath} directory not found, nothing to clear.");
        }


    }
}
