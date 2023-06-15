import argparse
import createKeyPlaylists

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ci', '--clientId', metavar='CLIENT ID', required=True, type=str)
    parser.add_argument('-cs', '--clientSecret', metavar='CLIENT SECRET', required=True, type=str)
    parser.add_argument('-r', '--redirectUri', metavar='REDIRECT URI', required=True, type=str)
    parser.add_argument('-u', '--userId', metavar='USER ID', required=True, type=str, help="Spotify user id. Same as username.")
    parser.add_argument('-p', '--playlistId', metavar='PLAYLIST ID', required=True, type=str)
    args = parser.parse_args()

    createKeyPlaylists.main(args.clientId, args.clientSecret, args.redirectUri, args.userId)

if __name__ == "__main__":
    main()