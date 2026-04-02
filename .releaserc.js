import fs from "fs";

export default {
  branches: [
     "main" // pre-release channel
  ],
  plugins: [
    ["@semantic-release/commit-analyzer", { preset: "conventionalcommits" }],
    ["@semantic-release/release-notes-generator", { preset: "conventionalcommits" }],
    ["@semantic-release/changelog", { changelogFile: "CHANGELOG.md" }],
    ["@semantic-release/git", {
      assets: ["CHANGELOG.md", "pyproject.toml"],
      message: "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
    }],
    ["@semantic-release/github"],
    {
      verifyRelease: async (context) => {
        const { nextRelease } = context;
         if (!nextRelease) {
          // Nothing to do if no release is determined
          return;
        }
        const file = "pyproject.toml";
        const pyproject = fs.readFileSync(file, "utf8");
        const updated = pyproject.replace(
          /version = ".*"/,
          `version = "${nextRelease.version}"`
        );
        fs.writeFileSync(file, updated);
      }
    }
  ]
};
