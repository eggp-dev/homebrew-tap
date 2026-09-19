cask "conn" do
  version "0.8.1"
  sha256 "6fa2b92989eb7537e6ebbb57e319ea35e73cc0f407aed0b393065a10df1d56d1"

  url "https://github.com/eggp-dev/conn/releases/download/v#{version}/conn-v#{version}-aarch64-apple-darwin-desktop.dmg"
  name "Conn"
  desc "Terminal you share with your AI agent, with approvals and takeover"
  homepage "https://github.com/eggp-dev/conn"

  livecheck do
    url "https://github.com/eggp-dev/conn/releases"
    regex(%r{/releases/tag/v(\d+(?:\.\d+)+)}i)
    strategy :page_match
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: ">= :monterey"

  app "Conn.app"

  zap trash: [
    "~/Library/Caches/dev.eggp.conn",
    "~/Library/Saved Application State/dev.eggp.conn.savedState",
    "~/Library/WebKit/dev.eggp.conn",
  ]

  caveats <<~EOS
    Conn keeps your profiles, policy and activity record in ~/.conn.
    They are left in place when you uninstall; remove that folder yourself if you want them gone.
    Connect your agent from Conn: Settings -> Agents -> Set up.
  EOS
end
