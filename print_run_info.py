import os
import sys
import uproot


def print_runinfo(root_file_path):
    """Print contents of trRunInfo tree from a ROOT file."""

    try:
        with uproot.open(root_file_path) as f:

            if "trRunInfo" not in f:
                print(f"[WARN] {root_file_path}: no trRunInfo tree found")
                return

            tree = f["trRunInfo"]

            # Read all branches as numpy arrays
            data = tree.arrays(library="np")

            print(f"\n=== {os.path.basename(root_file_path)} ===")

            for branch, values in data.items():
                # Usually run info has only one entry
                if len(values) == 1:
                    print(f"{branch}: {values[0]}")
                else:
                    print(f"{branch}: {values}")

    except Exception as e:
        print(f"[ERROR] Could not read {root_file_path}: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python print_runinfo.py <directory_with_root_files>")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a directory")
        sys.exit(1)

    root_files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".root")
    ]

    if not root_files:
        print("No ROOT files found in directory.")
        return

    for rf in sorted(root_files):
        print_runinfo(rf)


if __name__ == "__main__":
    main()


