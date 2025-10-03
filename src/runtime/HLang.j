.source HLang.java
.class public HLang
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is a [Ljava/lang/String; from Label0 to Label1
	iconst_2
	anewarray java/lang/String
	dup
	iconst_0
	ldc "nguyen"
	aastore
	dup
	iconst_1
	ldc "hieu"
	aastore
	astore_1
	aload_1
	iconst_0
	aaload
	aload_1
	iconst_1
	aaload
	invokevirtual java/lang/String/concat(Ljava/lang/String;)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	return
Label1:
.limit stack 5
.limit locals 2
.end method

.method public <init>()V
.var 0 is this LHLang; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	return
Label1:
.limit stack 1
.limit locals 1
.end method

.method public static <clinit>()V
Label0:
	return
Label1:
.limit stack 0
.limit locals 0
.end method
