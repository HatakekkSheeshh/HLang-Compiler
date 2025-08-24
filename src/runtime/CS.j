.source CS.java
.class public CS
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
	iconst_2
	istore_1
	iconst_3
	iload_1
	iadd
	istore_2
	iload_1
	iload_2
	iadd
	invokestatic io/print(I)V
	return
.limit stack 2
.limit locals 3
.end method

.method public <init>()V
	aload_0
	invokespecial java/lang/Object/<init>()V
	return
.limit stack 1
.limit locals 1
.end method
