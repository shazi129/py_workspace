
import sys
from google.protobuf.compiler import plugin_pb2 as plugin

def generate_code(request):
    response = plugin.CodeGeneratorResponse()
    for file in request.proto_file:
        # 对于每个.proto文件，生成一个输出文件
        output_file = response.file.add()
        output_file.name = file.name + ".txt"
        output_file.content = "This is a placeholder for generated code."
    return response

if __name__ == '__main__':
    # 从stdin读取CodeGeneratorRequest
    data = sys.stdin.buffer.read()
    request = plugin.CodeGeneratorRequest.FromString(data)

    # 生成代码
    response = generate_code(request)

    # 将CodeGeneratorResponse写入stdout
    sys.stdout.buffer.write(response.SerializeToString())