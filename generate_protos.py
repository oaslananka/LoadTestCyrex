
import os
import glob
import subprocess

def generate_protos(proto_dir, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    proto_files = glob.glob(os.path.join(proto_dir, "*.proto"))

    for proto_file in proto_files:
        command = [
            "python", "-m", "grpc_tools.protoc",
            f"-I={proto_dir}",
            f"--python_out={out_dir}",
            f"--grpc_python_out={out_dir}",
            proto_file
        ]
        subprocess.run(command, check=True)
        print(f"Compiled {proto_file} to {out_dir}")

if __name__ == "__main__":
    proto_dir = "src/protos/proto"
    out_dir = "src/protos"
    generate_protos(proto_dir, out_dir)
    print("All proto files have been compiled.")
