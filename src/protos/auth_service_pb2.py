# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import rpc_signin_user_pb2 as rpc__signin__user__pb2
import rpc_signup_user_pb2 as rpc__signup__user__pb2
import user_pb2 as user__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x61uth_service.proto\x12\x02pb\x1a\x15rpc_signin_user.proto\x1a\x15rpc_signup_user.proto\x1a\nuser.proto\".\n\x12VerifyEmailRequest\x12\x18\n\x10verificationCode\x18\x01 \x01(\t2\xc2\x01\n\x0b\x41uthService\x12\x38\n\nSignUpUser\x12\x13.pb.SignUpUserInput\x1a\x13.pb.GenericResponse\"\x00\x12;\n\nSignInUser\x12\x13.pb.SignInUserInput\x1a\x16.pb.SignInUserResponse\"\x00\x12<\n\x0bVerifyEmail\x12\x16.pb.VerifyEmailRequest\x1a\x13.pb.GenericResponse\"\x00\x42\x14Z\x12\x63yrex/vacancies/pbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\022cyrex/vacancies/pb'
  _globals['_VERIFYEMAILREQUEST']._serialized_start=84
  _globals['_VERIFYEMAILREQUEST']._serialized_end=130
  _globals['_AUTHSERVICE']._serialized_start=133
  _globals['_AUTHSERVICE']._serialized_end=327
# @@protoc_insertion_point(module_scope)